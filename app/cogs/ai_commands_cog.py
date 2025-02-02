import discord
from discord.ext import commands
from app.utils.ai_related.groq_api import send_to_groq
from app.utils.ai_related.groq_service import GroqService
from app.utils.ai_related.chatgpt_api import send_to_openai_vision
from app.utils.logger import logger


class AICommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.groq_service = GroqService()  
         

    @commands.command(name='ask', help="Ask a question to the AI.")
    async def ask(self, ctx, *, question):
        try:
            logger.debug(f"------- \nCommand ASK used by user {ctx.author.name}")
            messages = await self.groq_service.ask_question(ctx.author.name, question)
            response, _, _, _ = send_to_groq(messages)
            logger.debug(f"Sending response: {response}\n-------------")
            await ctx.send(response)
        except Exception as ex:
            logger.error(f"Error in Ask command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")
        
    

    @commands.command(name='chat', help="Chat with the AI.")
    async def chat(self, ctx, *, question: str):
        try:
            logger.debug(f"------- \nCommand CHAT used by user {ctx.author.name}")
            
            messages = await self.groq_service.assemble_chat_history(ctx, question)
            response, prompt_tokens, completion_tokens, total_tokens = send_to_groq(messages)
            logger.info(f"Prompt tokens: {prompt_tokens}")
            logger.info(f"Completion tokens: {completion_tokens}")
            logger.info(f"Total tokens: {total_tokens}")
            logger.debug(f"Sending response: {response}\n-------------")
            await ctx.send(response)
        except Exception as ex:
            logger.error(f"Error in Chat command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")

    @commands.command(name='vision', help="Ask a question to the AI with an image.")
    async def vision(self, ctx, *, question):
        try:
            logger.debug(f"------- \nCommand VISION used by user {ctx.author.name}")
            if ctx.message.attachments:
                attachment_url = ctx.message.attachments[0].url  # Get the first attachment's URL
                response, _, _, _ = send_to_openai_vision(question, attachment_url)
                logger.debug(f"Sending response: {response}\n-------------")
                await ctx.send(response)
            else:
                await ctx.send("No attachments found. Please upload an image with your question.")
        except Exception as ex:
            logger.error(f"Error in Vision command: {ex}")
            await ctx.send("Sorry, something went wrong while processing your request.")


async def setup(bot):
    await bot.add_cog(AICommands(bot))
