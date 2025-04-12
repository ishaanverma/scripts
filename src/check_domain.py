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
  try:
    response = requests.post(f"https://ntfy.sh/{ntfy_channel}", data=msg.encode())
    response.raise_for_status()
  except Exception as e:
    print(f"Failed to send notification: {str(e)}")


def main():
  if is_available():
    notify()


if __name__ == "__main__":
  main()
