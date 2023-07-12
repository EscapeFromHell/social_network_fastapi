import logging
from typing import Optional

import httpx
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import EmailStr

from src.config import settings
from src.core.schemas import ExtraUserFields
from src.utils import get_logger

logger = get_logger(__file__, logging.DEBUG)


class UserClient:
    def __prepare_data(self, data: dict) -> Optional[ExtraUserFields]:
        """
        Prepare additional user data from ClearBit API response.

        :param data: dict - ClearBit API response data.
        :return: Optional[ExtraUserFields] - Additional user fields (name, surname) or None if data is not available.
        """
        try:
            name = data["name"]["givenName"]
            surname = data["name"]["familyName"]
            return ExtraUserFields(name=name, surname=surname)

        except KeyError as error:
            logger.error(f"Error while processing the response from the ClearBit API: {error}")
            return None

    async def get_additional_data(self, email: EmailStr) -> Optional[ExtraUserFields]:
        """
        Get additional user data (name, surname) from ClearBit API.

        :param email: EmailStr - User's email.
        :return: Optional[ExtraUserFields] - Additional user fields (name, surname) or None if data is not available.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=settings.CLEARBIT_URL,
                    params={"email": email},
                    headers={
                        "Authorization": settings.CLEARBIT_API_KEY,
                        "Content-Type": "application/json",
                    },
                )

        except (httpx.ConnectError, httpx.ConnectTimeout) as error:
            logger.error(f"Error when accessing the ClearBit API: {error}")
            return None

        else:
            if response.is_error:
                logger.error(f"Error when accessing the ClearBit API: {response.content}")
                return None

            data = jsonable_encoder(response.json())
            extra_fields = self.__prepare_data(data=data)
            return extra_fields

    async def email_verifier(self, email: EmailStr) -> bool:
        """
        Verify if the specified email exists using EmailHunter API.

        :param email: EmailStr - Email to verify.
        :return: bool - True if the email is valid or if there was an error connecting to the EmailHunter API.
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    url=settings.EMAIL_HUNTER_URL,
                    params={"email": email, "api_key": settings.EMAIL_HUNTER_API_KEY},
                    headers={"Content-Type": "application/json"},
                )

        except (httpx.ConnectError, httpx.ConnectTimeout) as error:
            logger.error(f"Error when accessing the EmailHunter API: {error}")
            return True

        else:
            if response.is_error:
                logger.error(f"Error when accessing the EmailHunter API: {response.content}")
                return True

            data = jsonable_encoder(response.json())
            if data["data"]["status"] == "invalid":
                raise HTTPException(status_code=400, detail="The specified email does not exist")

            return True
