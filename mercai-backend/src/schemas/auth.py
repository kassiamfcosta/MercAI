"""
Schemas de validação para autenticação (Marshmallow)
"""

from marshmallow import Schema, fields, validate, ValidationError, validates
import re


class RegisterSchema(Schema):
    """
    Schema para validação de registro de usuário.
    """
    email = fields.Email(required=True, validate=validate.Length(max=255))
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=100),
        load_only=True
    )
    name = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        allow_none=True
    )
    
    @validates('password')
    def validate_password(self, value: str) -> None:
        """
        Valida formato da senha.
        
        Args:
            value: Senha para validar
            
        Raises:
            ValidationError: Se a senha não atender aos critérios
        """
        if len(value) < 8:
            raise ValidationError("A senha deve ter no mínimo 8 caracteres")
        
        # Verificar se contém pelo menos um número
        if not re.search(r'\d', value):
            raise ValidationError("A senha deve conter pelo menos um número")


class LoginSchema(Schema):
    """
    Schema para validação de login.
    """
    email = fields.Email(required=True)
    password = fields.Str(required=True, load_only=True)


class UserResponseSchema(Schema):
    """
    Schema para resposta de dados do usuário.
    """
    id = fields.Str()
    email = fields.Email()
    name = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()


class TokenResponseSchema(Schema):
    """
    Schema para resposta de token JWT.
    """
    success = fields.Bool()
    message = fields.Str()
    token = fields.Str()
    user = fields.Nested(UserResponseSchema, allow_none=True)

