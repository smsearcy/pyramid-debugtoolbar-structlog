structlog Panel for pyramid_debugtoolbar
========================================

Provide a panel to capture events logged via ``structlog`` and display them in the Pyramid DebugToolbar.


Demo
----

To check out the demonstration site:

.. code-block::

    git clone https://github.com/smsearcy/pyramid-debugtoolbar-structlog.git
    cd pyramid-debugtoolbar-structlog
    python -m venv venv
    venv/bin/activate
    pip install -e .[demo]
    cd demo
    python demo.py

Once running, browse to http://localhost:6543.
