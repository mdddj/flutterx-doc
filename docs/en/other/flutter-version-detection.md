# Flutter Version Detection

By default, when opening a Flutter project, a process will start and make an HTTP request to access the Flutter version information API.

Request URL

> URL: [https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json](https://storage.googleapis.com/flutter_infra_release/releases/releases_macos.json)

> The API requires a proxy to access

## Screenshot Preview

<<<<<<< HEAD
![image_9.png](../../assets/images/image_9.png)

![image_10.png](../../assets/images/image_10.png)
=======
![image_9.png](/images/image_9.png)

![image_10.png](/images/image_10.png)
>>>>>>> 9bd2974a6a06cdcd4b0cf104e44238350abd1f8a

"What's new" will redirect to the CHANGELOG.md file in the Flutter GitHub repository

## Feature Requirements - 2 Conditions Must Be Met

Version checking requires 2 conditions to be satisfied:

* Flutter command must be callable normally
* Must be able to access the above URL API normally

## Don't Need This Feature? Disable It Here

<<<<<<< HEAD
![image_8.png](../../assets/images/image_8.png)
=======
![image_8.png](/images/image_8.png)
>>>>>>> 9bd2974a6a06cdcd4b0cf104e44238350abd1f8a
