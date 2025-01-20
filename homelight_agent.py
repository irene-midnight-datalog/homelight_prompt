# AgentAI
from phi.agent import Agent
from phi.model.groq import Groq
from phi.model.openai import OpenAIChat
# Database
from phi.tools.postgres import PostgresTools
from phi.storage.agent.postgres import PgAgentStorage
# Email
from phi.tools import Toolkit
from imap_tools import MailBox, AND, OR
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from time import sleep
from dotenv import load_dotenv
import os

load_dotenv()

# ////////////////////////
#       Databases
# ////////////////////////
postgres_tools = PostgresTools(
    host="localhost",
    port=5432,
    db_name="homelight",
    user="igarciamontoya",
    password=""
)

storage = PgAgentStorage(
    table_name="agent_memory",
    db_url="postgresql+psycopg2://igarciamontoya:@localhost:5432/homelight"
    # postgresql://<username>:<password>@<host>:<port>/<database_name>
)

# ////////////////////////
#       Email
# ////////////////////////


class EmailReader(Toolkit):
    def __init__(self, email_address: str, email_password: str):
        super().__init__(name="email_reader")
        self.email_address: str = email_address
        self.email_password: str = email_password
        self.register(self.new_emails_reader)
        self.register(self.check_previous_emails)

    def check_previous_emails(self, agent_email: str = "defualt@gmail.com") -> str:
        """
        Connect to the email inbox to check if a particular email address has been contacted before.

        Args:
            agent_email (str): The email address of the person whose unread emails need to be retrieved.

        Returns:
            str
                Message that specifies if there has been previous contact with the email address or not
        """
        previous_contact = f"There is no previous emails with {agent_email}"

        with MailBox('imap.gmail.com').login(self.email_address, self.email_password) as mailbox:
            mailbox.folder.set("[Gmail]/All Mail")
            print(agent_email, '---', mailbox.folder.get())
            for _ in mailbox.fetch(reverse=True, limit=1, criteria=AND(to=agent_email), mark_seen=False):
                previous_contact = f"There has been previous emails with {agent_email}"
        return previous_contact

    def new_emails_reader(self, agent_email: str = "defualt@gmail.com") -> str:
        """
        Connect to the email inbox and fetch the contents of unread emails
        sent by a particular email address.

        Args:
            agent_email (str): The email address of the person whose unread emails need to be retrieved.

        Returns:
            str: A concatenated string of the contents of all unread emails sent by the specified agent_email.
                If no unread emails are found, returns an empty string.
        """
        contents = ''
        with MailBox('imap.gmail.com').login(self.email_address, self.email_password) as mailbox:
            print(agent_email, '---', mailbox.folder.get())
            for msg in mailbox.fetch(reverse=True, criteria=AND(seen=False, from_=agent_email)):
                print("New message")
                contents = contents + msg.text
        return contents


class EmailSender(Toolkit):
    def __init__(self, email_address: str, email_password: str):
        super().__init__(name="email_sender")
        self.email_address: str = email_address
        self.email_password: str = email_password
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.register(self.email_sender)

    def email_sender(self, agent_email: str = "moniregar@gmail.com", subject: str = "Hello friend", body: str = "Hello world", is_html: bool = False) -> str:
        """
        Sends an email to a specified recipient using the SMTP protocol.

        Parameters:
        -----------
        agent_email : str
            The recipient's email address. This is an email address fetched from the PostgreSQL database. Defaults to "default@gmail.com".
        subject : str
            The subject of the email. Defaults to "Hello friend".
        body : str
            The body content of the email. Defaults to "Hello world".
        is_html : bool, optional
            A flag to indicate whether the email body is HTML-formatted. If True, the body is sent as HTML.
            Defaults to False (plain text).

        Returns:
        --------
        str
            A message indicating whether the email was sent successfully or an error occurred.

        Exceptions:
        -----------
        If the email sending fails, the function will print the exception details and log the failure.
        """
        try:
            # Create the message
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = agent_email
            msg['Subject'] = subject

            # Attach the body text
            if is_html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))

            # Connect to the SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Start TLS encryption
                # Log in to the server
                server.login(self.email_address, self.email_password)
                server.send_message(msg)  # Send the email

            return "Email sent successfully!"

        except Exception as e:
            return f"Failed to send email: {e}"

# /////////////////////////////
#       Agentic Workflow
# /////////////////////////////


homelight_agent = Agent(
    name="Homelight Agent",
    model=OpenAIChat(id="gpt-4o"),
    tools=[postgres_tools,
           EmailSender(
               email_address="homelight.prompt@gmail.com",
               email_password=os.getenv("GMAIL_APP_PASSWORD")),
           EmailReader(
               email_address="homelight.prompt@gmail.com",
               email_password=os.getenv("GMAIL_APP_PASSWORD"))
           ],
    instructions=[f'''When using EmailSender, use the real estate agent's email
                    address fetched from the database for the agent_email
                    variable. Always sign the emails as Homelight Agentic AI.
                    Any SQL query must end with a semicolon.'''],
    storage=storage,
    add_history_to_messages=True,
    show_tool_calls=True,
    markdown=True,
)

if __name__ == '__main__':
    # First session
    agent_prompt = "Fetch from the postgres database the names of the real estate agents whose payments we have not collected yet. If there are multiple people, just pick the first one, if there none, stand by. Check your email and see if you have emailed the real estate agent (REA) before. If you have never contacted them, send them a friendly reminder with the payment information (listing address, listing price and commission percentage). If you have contacted the REA before, check if there are any new messages from them and read them, but if there aren’t new messages send another reminder.  If there are new messages from the REA and they are asking for more information about the payment, fetch the necessary information from the postgres database and send them a new email with the information. If there are new messages and the REA is promising to send their payment via check or another payment form, send an email thanking them, run a sql query to update the payment status of this listing in the database to 'True' and print the database table only including the real estate agents emails and payment status."
    postgres_prompt = "Fetch the contents of the clients referrals table and print them. After that, update the real estate agent's name to Irene Garcia for the row with id=4."
    # homelight_agent.print_response(agent_prompt, stream=True)
    try:
        while True:
            homelight_agent.print_response(agent_prompt, stream=True)
            sleep(60)

    except Exception as e:
        print(f"Error monitoring inbox: {e}")
    finally:
        print("End of monitoring")
