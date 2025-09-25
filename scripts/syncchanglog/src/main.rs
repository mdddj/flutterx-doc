use clap::Parser;
use serde::Deserialize;
use std::fs;
use std::path::PathBuf;
use anyhow::{Context, Result};

/// A tool to download a Markdown file from a URL and save it to local files.
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// URL of the Markdown file to download
    #[arg(short, long)]
    url: Option<String>,

    /// Paths to save the downloaded Markdown file to
    #[arg(short, long, num_args = 1..)]
    outputs: Vec<PathBuf>,

    /// Path to a configuration file (JSON or YAML)
    #[arg(short, long)]
    config: Option<PathBuf>,
}

#[derive(Deserialize, Debug, Default)]
struct Config {
    url: Option<String>,
    outputs: Option<Vec<PathBuf>>,
}

fn main() -> Result<()> {
    // 1. Parse command-line arguments
    let mut args = Args::parse();

    // 2. Load configuration from file if provided
    let mut config = Config::default();
    if let Some(config_path) = &args.config {
        let config_str = fs::read_to_string(config_path)
            .with_context(|| format!("Failed to read config file at {:?}", config_path))?;

        config = match config_path.extension().and_then(|s| s.to_str()) {
            Some("json") => serde_json::from_str(&config_str)
                .with_context(|| "Failed to parse JSON config")?,
            Some("yaml") | Some("yml") => serde_yaml::from_str(&config_str)
                .with_context(|| "Failed to parse YAML config")?,
            _ => anyhow::bail!("Unsupported config file format. Use .json or .yaml/.yml"),
        };
    }

    // 3. Merge arguments and config (CLI args take precedence)
    let url = args.url.or(config.url).context("A URL must be provided either via --url or a config file")?;
    if args.outputs.is_empty() {
        if let Some(outputs) = config.outputs {
            args.outputs = outputs;
        }
    }
    if args.outputs.is_empty() {
        anyhow::bail!("At least one output path must be provided either via --outputs or a config file");
    }


    // 4. Download the file content
    println!("Downloading from {}...", url);
    let response = reqwest::blocking::get(&url)?
        .error_for_status()
        .with_context(|| format!("Failed to download from URL: {}", url))?;

    let content = response.text()
        .with_context(|| "Failed to read response body as text")?;
    println!("Download successful.");


    // 5. Save the content to output files
    for output_path in &args.outputs {
        if let Some(parent) = output_path.parent() {
            fs::create_dir_all(parent)
                .with_context(|| format!("Failed to create directory structure for {:?}", output_path))?;
        }
        fs::write(output_path, &content)
            .with_context(|| format!("Failed to write to file {:?}", output_path))?;
        println!("Successfully saved to {:?}", output_path);
    }

    Ok(())
}
