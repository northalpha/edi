#!/usr/bin/env python
# -*- coding: utf-8 -*-

__title__ = "edi"
__version__ = "0.1"
__author__ = "Marcel Lauhoff"

from .core import Manager
from .decorators import edi_msg, edi_cmd, edi_msg_recv, edi_msg_recv_proto, edi_msg_recv_ircchan, edi_filter_msg_with_uflag, edi_filter_msg_without_uflag, edi_filter_msg_matches
