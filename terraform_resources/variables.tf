variable "region" {
  type = string
  default = "us-west-2"
  description = "region for aws"
}

variable "profile" {
  type = string
  default = "default"
  description = "profile alias for aws"
}

variable "arn" {
  type = string
  description = "arn of the lambda function to invoke"
}