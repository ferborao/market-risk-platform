terraform {
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# Create Bronze directory
resource "local_file" "bronze_dir_marker" {
  filename = "${var.project_root}/${var.bronze_path}.gitkeep"
  content  = ""
}

# Create Silver directory
resource "local_file" "silver_dir_marker" {
  filename = "${var.project_root}/${var.silver_path}.gitkeep"
  content  = ""
}

# Generate portfolio config file
resource "local_file" "portfolio_config" {
  filename = "${var.project_root}/config/portfolio.json"
  content  = jsonencode({
    tickers     = var.tickers
    bronze_path = var.bronze_path
    silver_path = var.silver_path
  })
}