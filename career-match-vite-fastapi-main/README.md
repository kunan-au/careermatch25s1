# Career Match

## Description

Career Match is a revolutionary new job search information service platform that matches job searchers based on their talents and preferences. Job seekers only need to build a profile on the Career Match platform, which includes a CV, wage expectations, and career goals, to receive job listings for relevant employment.
In terms of technological implementation, Career Match members filter job applicants' information by keywords to match the best candidates with open positions using machine learning technology and natural language processing models.

Legacy project repository: https://gitlab.com/hideontree/grow_right


## Project Startup Guide

### A. First Set-up and Starting the Project

#### 1. Git the code from Gitlab page [https://gitlab.com/yupeiyuan0108/career-match-vite-fastapi](https://gitlab.com/yupeiyuan0108/career-match-vite-fastapi).

#### 2. Open the folder `career-match-vite-fastapi` in Visual Studio Code.

#### 3. Open Docker Desktop.

#### 4. Open a _new_ terminal on VSCode and input those commands to activate backend:

```bash
cd server
cp .env.example .env
docker network create app_main
docker-compose up -d --build
```
Those commands are just for **_first set-up_**.

And after doing that, you shall see 3 new containers has been added on Docker.

#### 5. Start all three containers: `app`,`app_db`, `app_redis` on Docker.

If you are a Windows system user, you may not able to open this container:  `app`

Please click [D-issues-you-may-face](#d-issues-you-may-face) for further information.



#### 6. Open a new terminal on VSCode and input those commands to activate frontend:

```bash
cd client
npm install # Install the dependencies
npm run dev # Start the development server
```

Now you shall see below showing:
> career-match@0.0.0 dev
> 
> vite

  ➜  Local:   http://localhost:5173/

  ➜  Network: use --host to expose

  ➜  press h + enter to show help
  
#### 7. Copy the link and paste it in a browser.

Now you shall see our page.

### B. Running Project

Just follow those steps:

#### 1. Open the folder `career-match-vite-fastapi` in Visual Studio Code.

#### 2. Open Docker Desktop and start all three containers.

#### 3. Open a _new_ terminal on VSCode and input those commands:

```bash
cd client
npm install 
npm run dev
```
#### 4. Copy the link and paste it in a browser.

### C. Navigating the Interface

#### 1. All features are available only after logging in.

You should sign up first and then you can log in.

Here is an example account for you to sign up:

Account name:

> user@example.com

Password:

> CareerMatch1234!

#### 2. Switch to Different Pages

Click [client\src\router.tsx](client\src\router.tsx) for different pages link name.

If you are still in gitlab page, click [client/src/router.tsx](client/src/router.tsx) for different pages link name.

For example, if you want to switch to user profile page, the link should be like this:
> http://localhost:5173/profile

#### 3. Shut down the project.

Press Ctrl and C:
> ^C ^CTerminate batch job (Y/N)? 

Then press y.

### D. Issues you may face
#### 1. Fail to start all 3 containers for Windows users:
Follow these steps:

(1) Locate and delete the career-match-vite-fastapi folder on your computer.

(2) Open the Command Prompt on Windows(cmd) and navigate to the directory where you want to place the project folder.

(3) Enter the command:


```bash
git config --global core.autocrlf input 
git clone https://gitlab.com/yupeiyuan0108/career-match-vite-fastapi.git
```

This step is designed to ensure that when cloning the project, LF (Unix-style) line endings are preserved instead of CRLF (Windows-style). It is necessary to set the `core.autocrlf` option accordingly.

(4) Open Docker Desktop.

(5) Open Visual Studio Code and perform the initial configuration (first set-up) to activate the backend.

(6) Check Docker, and you should see that all containers are now running correctly.


#### 2. Fail to install npm:
Check if you have sudo client folder.

#### 3. Fail to SignUp/in
When attempting to sign up or sign in a user, you might encounter the following error message:

> Something went wrong connecting to the server. Please try again later.

Follow these steps:

(1)Apply database migrations:

Enter the following commands in VScode:

```bash
cd server
docker-compose run app alembic upgrade head
docker-compose down
docker-compose up -d --build
```

(2)Restart the development server:

```bash
cd client
npm run dev
```
### E. Further Information

[Backend Readme](server\README.md)

[Frontend Readme](clinet\README.md)

If you are still in gitlab page, click: 


[Backend Readme](server/README.md)

[Frontend Readme](clinet/README.md)


for further information.


