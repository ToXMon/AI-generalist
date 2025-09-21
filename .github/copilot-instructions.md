Rule 1: Start with a Clear Project Structure
•	Organize your project into meaningful directories like `backend`, `frontend`, `database` (or `db`), and `proxy`. This helps you and others understand what's where (1:19:29).
•	Sub-categorize within these, e.g., `backend/nodejs`, `backend/php`, `frontend/react`, etc., for clarity (1:22:01).

•	Rule 2: Make Your Project Self-Contained with Docker Compose
•	Your project should "just work" by running `docker compose up --build`. It should include everything needed to spin up the application for development, including databases and sample data (1:24:58).
•	Use Docker Compose to define your entire service stack (web server, databases, APIs, etc.) and how they interact (3:33:53). It describes multiple containers working together.

•	Rule 3: Use Docker Init for Best Practices
•	For new projects, use `docker init` to automatically generate a `Dockerfile`, `docker-compose.yml`, and `.dockerignore` file. This ensures you follow current best practices for containerization (2:27:28).

•	Rule 4: Optimize Dockerfile Development with Interactive Shells (Exec)
•	When building a Docker image, start an interactive container (`docker run -it <image> bash/sh`) and test commands live. Once a command works, copy it to your `Dockerfile` (2:44:46). This is much more efficient than repeatedly running `docker build`.
•	Remember `docker exec` to jump into a running container to debug issues (2:21:05).

•	Rule 5: Leverage Docker Desktop for Productivity
•	Use Docker Desktop's UI for quick insights into running containers, logs, and `inspect` details (1:09:56).
•	Utilize its search feature (`Ctrl/Cmd+K`) to easily find official images, tags, and documentation on Docker Hub without leaving the app (3:08:44).

•	Rule 6: Understand Bind Mounts vs. Docker Compose Watch
•	Bind Mounts: Directly link a local directory to a container's path. Changes on either side sync automatically, which can be dangerous for accidental deletions (2:17:35).
•	Docker Compose Watch: Offers safer development. In "sync" mode, it copies local changes into the container (no automatic sync back). In "build" mode, it rebuilds the image on file changes (2:23:34).

•	Rule 7: Use Multi-Stage Builds for Leaner Images
•	Separate your build environment from your runtime environment. For example, use a Node.js image to build your React app, then copy only the static build output to a small NGINX container (3:21:59). This keeps your final production images small and secure.

•	Rule 8: Automate with Scripts and Documentation
•	If some setup steps can't be in your `docker-compose.yml` (e.g., fetching sensitive credentials), automate them with shell scripts or document them clearly in a `README` file (3:31:52). Automation doubles as documentation.

•	Rule 9: Embrace NGINX Unit for Simpler PHP/Polyglot Deployments
•	Instead of separate NGINX and PHP-FPM containers, consider NGINX Unit to run multiple languages (like PHP and Node.js) and act as a web server within a single container (3:19:30).