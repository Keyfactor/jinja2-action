FROM dinutac/jinja2docker:2.1.3

RUN pip install \
    Jinja2==3.0.3 \
    j2cli==0.3.10 \
    pyyaml==5.3.1 \
    MarkupSafe==2.0.1

COPY entrypoint.py /entrypoint.py

ENTRYPOINT ["/entrypoint.py"]

