# Bots for Diamonds Minigame

Creating bots for **Diamonds** minigame with **Greedy Algorithm**.

## What is Diamonds ?

Diamonds is a minigame with an objective to hunt diamonds as many as you can.

## Greedy Algorithm Implementation

lorem.

---

## How to Run the Game Engine

You only need to do the **Requirements** and **Set Up** section once. After that, you can skip to **Run** section.

### Requirements

- [Node.js](https://nodejs.org/en)

- [Docker desktop](https://www.docker.com/products/docker-desktop/)

- Yarn  
  Node.js installation comes with npm.  
  Install yarn with npm using following command:

  ```
  npm install --global yarn
  ```

### Set Up

1. Clone this repository

   ```
   git clone https://github.com/bastianhs/Tubes1_OogoeDiamonds.git
   ```

2. Go to the parent directory

   ```
   cd Tubes1_OogoeDiamonds
   ```

3. Go to the game engine directory

   ```
   cd src/tubes1-IF2211-game-engine-1.1.0
   ```

4. Install dependencies with yarn  
   (if root-workspace error log "husky - .git can't be found" arise, the program can still be run)

   ```
   yarn
   ```

5. Set up default environment variable

   - For windows

   ```
   ./scripts/copy-env.bat
   ```

   - For linux / (possibly) macOS

   ```
   chmod +x ./scripts/copy-env.sh
   ./scripts/copy-env.sh
   ```

6. Set up local database with docker

   Open docker desktop, then run the following command:

   ```
   docker compose up -d database
   ```

   After that, run the following script:  
   (if root-workspace error log "husky - .git can't be found" arise, the program can still be run)

   - For windows
     ```
     ./scripts/setup-db-prisma.bat
     ```
   - For Linux / (possibly) macOS
     ```
     chmod +x ./scripts/setup-db-prisma.sh
     ./scripts/setup-db-prisma.sh
     ```

7. Build
   ```
   npm run build
   ```

### Run

If you have done the previous sections, you can skip to this step to run the game engine. Make sure that you are in the **tubes1-IF2211-game-engine-1.1.0** directory.

```
npm run start
```

---

## How to Run the Bots

You only need to do the **Requirements** and **Set Up** section once. After that, you can skip to **Run** section.

### Requirements

- [Python](https://www.python.org/downloads/)

### Set Up

1. Open new terminal, then go to the bot directory  
   If you are in **Tubes1_OogoeDiamonds** directory, use the following command:

   ```
   cd src/tubes1-IF2211-bot-starter-pack-1.0.1
   ```

2. Install dependencies with pip

   ```
   pip install -r requirements.txt
   ```

### Run

- For windows

  ```
  ./run-bots.bat
  ```

- For Linux / (possibly) macOS

  ```
  ./run-bots.sh
  ```

---

## Author

Group name: Oogoe Diamonds

1. [Agil Fadillah Sabri](https://github.com/Agil0975)  
   13522006

2. [Bastian H. Suryapratama](https://github.com/bastianhs)  
   13522034

3. [Haikal Assyauqi](https://github.com/Haikalin)  
   13522052
