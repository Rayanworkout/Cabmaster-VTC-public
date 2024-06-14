# Cabmaster's website.

I am using **Django** for backend as well as its template language.
The front-end is made with **HTML / CSS** and enhanced with vanilla **Javascript**.

User inputs are controlled with **Javascript**, and form submissions / requests are sent through **Javascript** in order not to require a page reload.

The website has a showcase site as well as many pages, an admin dashboard and a partner dashboard panel. They can login and add / modify
entries in the database **(CRUD)**.

The database used is **SQLITE3** but I could use **MariaDB**. Unfortunately the server is not powerful enough.

The project is deployed to an **AWS** Debian 12 server (EC2 Micro Instance).

CI/CD is managed through **Github Actions** and **Jenkins**. All **Tests (unit, integration and end-to-end)** are run with **Github Actions** thanks to a 
**.yaml** file. I also generate a tests report coverage with **Coverage**.

When the Dev branch is merged with the Main branch, github sends a webhook to **Jenkins**, and **Jenkins** deploys the website to the server.

I get success / errors alerts for each deploy to ensure everything goes right.

On the server the project is run by **Apache2** server