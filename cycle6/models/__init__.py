"""
Komodo Hub - Models Package
All database models for the Komodo Hub system
"""

from .user_models import User, Organization, OrganizationMember, UserProfile
from .class_models import Class, ClassEnrollment, Activity, Submission, Assessment
from .program_models import (Program, ProgramEnrollment, ContentLibrary,
                             SpeciesSighting, CreativeCanvas, Message, Note)
from .analytics_models import AccessLog, BusinessAnalytics

__all__ = [
    # User models
    'User',
    'Organization',
    'OrganizationMember',
    'UserProfile',

    # Class models
    'Class',
    'ClassEnrollment',
    'Activity',
    'Submission',
    'Assessment',

    # Program models
    'Program',
    'ProgramEnrollment',
    'ContentLibrary',
    'SpeciesSighting',
    'CreativeCanvas',
    'Message',
    'Note',

    # Analytics models
    'AccessLog',
    'BusinessAnalytics'
]

__version__ = '1.0.0'
__author__ = 'Rick Ting Wang'