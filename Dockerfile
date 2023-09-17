FROM dominator454/DOMINATORXBOT/:latest

RUN git clone https://github.com/dominator454/DOMINATORXBOT.git /root/DominatorBot

WORKDIR /root/DominatorBot

RUN pip3 install -U -r requirements.txt

ENV PATH="/home/DominatorBot/bin:$PATH"

CMD ["python3", "-m", "DominatorBot"]
