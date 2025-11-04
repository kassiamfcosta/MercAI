"""
Schemas de Autenticação - Validação

Módulo contendo schemas Marshmallow para validação de dados de autenticação.
"""

from marshmallow import Schema, fields, validate, ValidationError


class RegisterSchema(Schema):
    """
    Schema para validação de registro de usuário.
    """
    
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'O email é obrigatório',
            'invalid': 'Email inválido'
        }
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=8, max=100),
        error_messages={
            'required': 'A senha é obrigatória',
            'invalid': 'A senha deve ter entre 8 e 100 caracteres'
        }
    )
    name = fields.Str(
        required=False,
        validate=validate.Length(max=100),
        error_messages={
            'invalid': 'O nome deve ter no máximo 100 caracteres'
        }
    )


class LoginSchema(Schema):
    """
    Schema para validação de login.
    """
    
    email = fields.Email(
        required=True,
        error_messages={
            'required': 'O email é obrigatório',
            'invalid': 'Email inválido'
        }
    )
    password = fields.Str(
        required=True,
        error_messages={
            'required': 'A senha é obrigatória'
        }
    )

