####################################################################################################
#
# ImageBrowser — ...
# Copyright (C) 2024 Fabrice SALVAIRE
# SPDX-License-Identifier: GPL-3.0-or-later
#
####################################################################################################

# uvicorn test-image-server:app --reload
# http://127.0.0.1:8000/docs

####################################################################################################

from ImageBrowser.library.logging import setup_logging
logger = setup_logging()

from ImageBrowser.backend.ImageCollection.ImageServer import ImageServer

####################################################################################################

image_server = ImageServer()
app = image_server.app
