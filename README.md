# homelight_prompt

## Prompt:
HomeLight refers clients to Real Estate Agents, and collects a percentage of the agent commissions if the client ends up closing a real estate transaction with the agent.
Design an operational flow using AI tools that exist today to do the following: 
+ (1) Identify if the referral closed with that agent, 
+ (2) Inform the agent about collections, and 
+ (3) Actually collect on the commission amount.
### Notes:
+ Please showcase process flows and types of tools/platforms you would use to construct this.
+ Any sort of prototypes using AI Agents highly encouraged.
+ Spend no more than 2 hours on this assignment.

## Media

+ [Google Slides](https://docs.google.com/presentation/d/1_80b99QuUklZXiWYUTqKcES_oJWdn5KnCqCZff22U88/edit?usp=sharing)
+ [Video demonstration](https://youtu.be/DoHkLoj8HPY)

## Agent Logic

![AI Logic](https://github.com/irene-midnight-datalog/homelight_prompt/blob/main/ai_logic.png)

Fetch from the postgres database the names of the real estate agents whose payments we have not collected yet. If there are multiple people, just pick the first one. Check your email and see if you have emailed the real estate agent (REA) before. If you have never contacted them, send them a friendly reminder with the payment information (listing address, listing price and commission percentage). 

If you have contacted the REA before, check if there are any new messages from them and read them, but if there aren’t new messages send another reminder. 

If there are new messages from the REA and they are asking for more information about the payment, fetch the necessary information from the postgres database and send them a new email with the information.

If there are new messages and the REA is promising to send their payment via check or another payment form, send an email thanking them, run a sql query to update the payment status of this listing in the database to 'True' and print the database table only including the real estate agents emails and payment status. 
