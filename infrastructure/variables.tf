variable "project_root" {
  description = "Absolute path to project root"
  type        = string
}

variable "bronze_path" {
  description = "Path to Bronze layer"
  type        = string
  default     = "data/bronze/"
}

variable "silver_path" {
  description = "Path to Silver layer"
  type        = string
  default     = "data/silver/"
}

variable "tickers" {
  description = "List of equity tickers in the portfolio"
  type        = list(string)
  default     = ["BBVA.MC", "SAN.MC", "CABK.MC", "JPM", "GS", "AAPL", "MSFT", "REP.MC", "XOM", "SPY"]
}
