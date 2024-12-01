"""Gateways Package.

This package contains adapters responsible for interacting with external systems and services,
acting as gateways between the application's core domain and the outside world.

Key responsibilities:

* Data persistence: Implement gateways to interact with databases or other storage mechanisms,
 enabling the persistence and retrieval of domain entities.
* External communication: Provide gateways to communicate with external APIs,
 services, or message queues, facilitating integration with third-party systems.
* File handling: Offer gateways for file operations, such as reading, writing, and processing files.
* Other external interactions: Handle any other interactions with external resources or systems
  required by the application.
"""

from .app import app

__all__ = ["app"]
