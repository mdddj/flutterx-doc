# Freezed 3.x Version Migration Tool

Freezed 3.0 has changes that require adding the `sealed` or `abstract` keyword before the class.

Since my own project makes extensive use of freezed, I created this tool to facilitate migration from version 2.0 to 3.0, otherwise you'd have to modify a large number of classes.

> **Note** It will display an action notification bar at the top of your editor. If it shows up due to a bug, you can close it.

![image_16.png](../../assets/images/image_16.png)

It supports modifying the current file as well as scanning and modifying the entire project.

> **Note**

![image_17.png](../../assets/images/image_17.png)