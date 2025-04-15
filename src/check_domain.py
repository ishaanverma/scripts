import os
import requests

domain = os.environ["DOMAIN"]
ntfy_channel = os.environ["NTFY_CHANNEL"]

def is_available():
  # check if domain is available using google registry
  url = f"https://www.registry.google/rdap/domain/{domain}"
  response = requests.get(url)

  return response.status_code == 404


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
  else:
    print("Not available")


if __name__ == "__main__":
  main()
