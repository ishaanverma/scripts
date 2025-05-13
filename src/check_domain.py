import os
import requests

domain = os.environ["DOMAIN"]
ntfy_channel = os.environ["NTFY_CHANNEL"]

def is_available():
  # Check if domain is available using RDAP
  # Use rdap.org which redirects to the appropriate registrar's RDAP server
  url = f"https://rdap.org/domain/{domain}"
  
  try:
    response = requests.get(url)
    
    # If status code is 404, the domain likely doesn't exist in the registry
    # This is the most reliable indicator that a domain is available for registration
    if response.status_code == 404:
      return True
      
    # If we get a successful response (200), the domain exists in the registry
    # and is NOT available for fresh registration
    return False
  except Exception as e:
    print(f"Error checking domain availability: {str(e)}")
    # On error, don't trigger notifications
    return False


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
    print("Domain is not available for registration")


if __name__ == "__main__":
  main()
