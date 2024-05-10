# Foxexpress-bot-python

Foxexpress-bot-python is a toolkit to automate the delivery status of the parcel managed by the Fox-express delivery service in Russia.

## Installation

Install Python 3.
Install all dependencies via pip:

```bash
pip install smtplib requests bs4 pytz
```

Clone this rep to your machine.

```bash
git clone https://github.com/kashamalasha/foxexpress-bot-python.git
```

## Content

Toolkit includes the following files:

* `fox.py` - Python script to find updates and send them via email.
* `foxtabs.py` - Python script to display the latest status in the terminal.
* `fox.ini` - Template of the configuration file for data requesting and email sending.
* `crontab.txt` - Example of a crontab configuration for recurring execution.

## Usage

1. Specify your settings in the `fox.ini` file according to your requirements.
2. Execute `foxtabs.py` to initiate the request to Fox-express.
3. Run `fox.py` to ensure that the email settings are properly configured.
4. Edit `crontab -e` to define the schedule for requests.
5. Monitor the updates in the receiver mailbox specified in the `fox.ini` file.

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

None