resource "aws_security_group" "bad_ssh" {
  name        = "bad-ssh"
  description = "INTENTIONAL: insecure for tfsec learning"

  ingress {
    description = "SSH open to the world (bad)"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/16"]
  }
}