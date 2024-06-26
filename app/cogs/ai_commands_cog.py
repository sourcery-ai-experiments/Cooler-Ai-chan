import discord
from discord.ext import commands
from app.utils.ai_related.groq_api import send_to_groq
from app.utils.ai_related.chatgpt_api import send_to_openai
from app.utils.ai_related.groq_service import GroqService
from app.utils.ai_related.chatgpt_api import send_to_openai_vision
from app.utils.logger import logger
from app.utils.command_utils import custom_command

class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.groq_service = GroqService()  
         

    @custom_command(name='ask', help="Ask a question to the AI.")
    async def ask(self, ctx, *, question):
        try:
            logger.debug(f"------- \nCommand ASK used by user {ctx.author.name}")
            messages = await self.groq_service.ask_question(ctx.author.name, ctx.author.id, question)
            response, _, _, _ = send_to_groq(messages)
            logger.debug(f"Sending response: {response}\n-------------")
            await ctx.send(response)
        except Exception as ex:
            logger.error(f"Error in Ask command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")
        
    

    @custom_command(name='chat', help="Chat with the AI.")
    async def chat(self, ctx, *, question: str):
        try:
            logger.debug(f"------- \nCommand CHAT used by user {ctx.author.name}")
            messages = await self.groq_service.assemble_chat_history(ctx)
            messages = await self.groq_service.add_command_messages(ctx, messages, question)
            response, prompt_tokens, completion_tokens, total_tokens = send_to_groq(messages)
            logger.info(f"Prompt tokens: {prompt_tokens}")
            logger.info(f"Completion tokens: {completion_tokens}")
            logger.info(f"Total tokens: {total_tokens}")
            logger.debug(f"Sending response: {response}\n-------------")
            await ctx.send(response)
        except Exception as ex:
            logger.error(f"Error in Chat command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")

    @custom_command(name='oldask', help="Ask a question to the AI.")
    async def oldask(self, ctx, *, question):
        try:
            logger.debug(f"------- \nCommand ASK used by user {ctx.author.name}")
            messages = await self.groq_service.ask_question(ctx.author.name, ctx.author.id, question)
            response, _, _, _ = send_to_openai(messages)
            logger.debug(f"Sending response: {response}\n-------------")
            await ctx.send(response)
        except Exception as ex:
            logger.error(f"Error in Ask command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")
        
    

    @custom_command(name='oldchat', help="Chat with the AI.")
    async def oldchat(self, ctx, *, question: str):
        try:
            logger.debug(f"------- \nCommand CHAT used by user {ctx.author.name}")
            
            messages = await self.groq_service.assemble_chat_history(ctx)
            messages = await self.groq_service.add_command_messages(ctx, messages, question)
            response, prompt_tokens, completion_tokens, total_tokens = send_to_openai(messages)
            logger.info(f"Prompt tokens: {prompt_tokens}")
            logger.info(f"Completion tokens: {completion_tokens}")
            logger.info(f"Total tokens: {total_tokens}")
            logger.debug(f"Sending response: {response}\n-------------")
            await ctx.send(response)
        except Exception as ex:
            logger.error(f"Error in Chat command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")

    @commands.hybrid_command(name='vision', help="Ask a question to the AI with an image.")
    async def vision(self, ctx, question: str, attachment: discord.Attachment = None):
        try:
            logger.debug(f"------- \nCommand VISION used by user {ctx.author.name}")
            
            # Check if an attachment was provided
            if attachment is None and ctx.message.attachments:
                attachment = ctx.message.attachments[0]

            if attachment:
                await ctx.defer()  # Defer the response to avoid timeout
                attachment_url = attachment.url  # Get the attachment's URL
                
                # Correctly await and unpack the response
                response = await send_to_openai_vision(question, attachment_url)
                
                if isinstance(response, tuple):
                    response, _, _, _ = response

                logger.debug(f"Sending response: {response}\n-------------")
                
                # Split the response into chunks if it exceeds the Discord message limit
                if len(response) > 2000:
                    for i in range(0, len(response), 2000):
                        await ctx.send(response[i:i+2000])
                else:
                    await ctx.send(response)
            else:
                await ctx.send("No attachments found. Please upload an image with your question.")
        except Exception as ex:
            logger.error(f"Error in Vision command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")


async def setup(bot):
    await bot.add_cog(AICommands(bot))
