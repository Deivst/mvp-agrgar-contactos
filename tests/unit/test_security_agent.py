"""
Tests unitarios para SecurityAgent.
"""

import pytest
from unittest.mock import AsyncMock

from src.agents.security_agent import SecurityAgent


class TestSecurityAgent:
    """Tests para SecurityAgent."""

    @pytest.fixture
    def agent(self, mock_gemini_service):
        """Fixture que provee una instancia del agente."""
        return SecurityAgent(
            gemini_service=mock_gemini_service,
            allowed_users=[123456789]
        )

    @pytest.mark.asyncio
    async def test_should_process_valid_request_from_authorized_user(
        self,
        agent,
        sample_telegram_message,
        mock_gemini_response_success
    ):
        """Verifica procesamiento exitoso de usuario autorizado."""
        # Arrange
        agent.gemini_service.extract_contact_info.return_value = mock_gemini_response_success

        # Act
        result = await agent.process_request(sample_telegram_message)

        # Assert
        assert result["success"] is True
        assert "contact" in result
        agent.gemini_service.extract_contact_info.assert_called_once()

    @pytest.mark.asyncio
    async def test_should_reject_unauthorized_user(self, agent):
        """Verifica rechazo de usuario no autorizado."""
        # Arrange
        message = {
            "text": "Test message",
            "user_id": 999999999,  # Usuario no autorizado
            "chat_id": 123,
            "username": "unauthorized"
        }

        # Act
        result = await agent.process_request(message)

        # Assert
        assert result["success"] is False
        assert result["error_type"] == "unauthorized"
        assert "autorización" in result["error"].lower()

    @pytest.mark.asyncio
    async def test_should_reject_short_message(self, agent):
        """Verifica rechazo de mensaje muy corto."""
        # Arrange
        message = {
            "text": "Hi",
            "user_id": 123456789,
            "chat_id": 123,
            "username": "testuser"
        }

        # Act
        result = await agent.process_request(message)

        # Assert
        assert result["success"] is False
        assert result["error_type"] == "invalid_message_format"

    @pytest.mark.asyncio
    async def test_should_handle_gemini_extraction_failure(
        self,
        agent,
        sample_telegram_message,
        mock_gemini_response_failure
    ):
        """Verifica manejo de falla en extracción de Gemini."""
        # Arrange
        agent.gemini_service.extract_contact_info.return_value = mock_gemini_response_failure

        # Act
        result = await agent.process_request(sample_telegram_message)

        # Assert
        assert result["success"] is False
        assert result["error_type"] == "extraction_failed"

    def test_should_add_user_to_whitelist(self, agent):
        """Verifica agregar usuario a whitelist."""
        # Arrange
        new_user_id = 777777777

        # Act
        agent.add_user(new_user_id)

        # Assert
        assert new_user_id in agent.allowed_users

    def test_should_remove_user_from_whitelist(self, agent):
        """Verifica remover usuario de whitelist."""
        # Arrange
        user_id = 123456789

        # Act
        agent.remove_user(user_id)

        # Assert
        assert user_id not in agent.allowed_users

    def test_should_block_user(self, agent):
        """Verifica bloqueo de usuario."""
        # Arrange
        user_id = 123456789

        # Act
        agent.block_user(user_id)

        # Assert
        assert user_id in agent.blocked_users

    @pytest.mark.asyncio
    async def test_should_reject_blocked_user(self, agent):
        """Verifica rechazo de usuario bloqueado."""
        # Arrange
        user_id = 123456789
        agent.block_user(user_id)

        message = {
            "text": "Test message",
            "user_id": user_id,
            "chat_id": 123,
            "username": "testuser"
        }

        # Act
        result = await agent.process_request(message)

        # Assert
        assert result["success"] is False
        assert result["error_type"] == "unauthorized"
        assert "bloqueado" in result["error"].lower()
