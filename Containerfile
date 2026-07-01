FROM ubuntu

RUN apt update && apt install fish vim python3 python3-venv less -y
RUN /usr/bin/fish -c "set -U fish_greeting"
RUN echo fish > /root/.bashrc
RUN echo "source venv/bin/activate.fish" >> /root/.config/fish/config.fish
WORKDIR /root/cyberscan
COPY cyberscan cyberscan/
COPY data data/
COPY __init__.py .
COPY tests tests/
COPY packages.txt .
RUN python3 -m venv venv && ./venv/bin/pip install -r packages.txt
