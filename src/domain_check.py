import os
import subprocess
import requests

domain = os.environ["DOMAIN"]
whois_server = os.environ["WHOIS_SERVER"]
ntfy_channel = os.environ["NTFY_CHANNEL"]

def is_available():
  result = subprocess.run(
    [
      "whois",
      "-h",
      whois_server,
      domain,
    ],
    capture_output=True,
    text=True
  )

  return "Domain not found" in result.stdout


def notify():
  msg = "domain is AVAILABLE!"
  requests.post(f"https://ntfy.sh/{ntfy_channel}", data=msg.encode())


def main():
  if is_available():
    notify()


if __name__ == "__main__":
  main()
