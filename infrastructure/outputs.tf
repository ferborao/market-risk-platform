output "bronze_path" {
  description = "Path to Bronze layer"
  value       = "${var.project_root}/${var.bronze_path}"
}

output "silver_path" {
  description = "Path to Silver layer"
  value       = "${var.project_root}/${var.silver_path}"
}

output "portfolio_config_path" {
  description = "Path to the generated portfolio config file"
  value       = "${var.project_root}/config/portfolio.json"
}