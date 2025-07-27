FROM squidfunk/mkdocs-material:latest

# Install additional plugins
RUN pip install \
    mkdocs-mermaid2-plugin \
    mkdocs-pdf-export-plugin \
    mkdocs-git-revision-date-localized-plugin \
    mkdocs-minify-plugin \
    mkdocs-redirects

# Set working directory
WORKDIR /docs

# Default command
CMD ["serve", "--dev-addr=0.0.0.0:8000"]
