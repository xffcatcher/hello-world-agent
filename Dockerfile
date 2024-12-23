# Use the skynet-runtime-java as the base image
FROM xfireflycatcher/skynet-runtime-java:latest

# Set the working directory
WORKDIR /agent

# Create required directories
RUN mkdir -p libs spec

# Copy the thin JAR to the libs folder
COPY build/agent/libs/*.jar libs/

# Copy dependencies to the libs folder
COPY build/agent/dependencies/*.jar libs/

# Copy the agent.spec file to the spec folder
COPY agent.spec spec/

WORKDIR /workspace
# Set the entry point with -cp option
# ENTRYPOINT ["java", "--add-opens", "java.base/java.net=ALL-UNNAMED", "-jar", "/app/app.jar"]
