from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, ForeignKey, LargeBinary, text
from src.database import Base
from sqlalchemy.dialects.mysql import INTEGER, TINYINT, TIMESTAMP
#from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy.sql import func


class BrandSettings(Base):
    __tablename__ = 'brand_settings'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    brand_id = Column(Integer, nullable=False)
    settings_json = Column(Text, nullable=False)
    inactive_settings = Column(Boolean, default=False)
    created_by = Column(Integer, nullable=False)
    created_time = Column(TIMESTAMP, nullable=False, server_default='CURRENT_TIMESTAMP') #onupdate='CURRENT_TIMESTAMP')

class Story(Base):
    __tablename__="story"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=True)
    summary = Column(Text)
    #guide_id = Column(Integer, ForeignKey('video.id'), nullable=True)
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    category_id = Column(Integer, nullable=True)
    inactive = Column(Boolean, nullable=False, default=False)
    created_time = Column(DateTime, default=datetime.utcnow)
    background = Column(Text)
    description = Column(Text)
    is_private = Column(Boolean, default=True)
    story_type = Column(Integer, default=1)  # 1=Video, 2=ScreenShare, 3=Audio, 4=Chat
    approval_preferred = Column(Boolean, default=False)
    purpose = Column(String(255), nullable=True)
    timing = Column(String(255), nullable=True)
    distribution = Column(String(255), nullable=True)
    promoted_to_team = Column(Boolean, default=False)
    recording = Column(Boolean, nullable=False, default=False)  # 0=Standard, 1=Interactive
    difficulty = Column(Integer, nullable=False, default=0)  # 0=General, 1=Low/Easy, 2=Medium, 3=Hard/High
    interactive_pattern = Column(Integer, nullable=False, default=2)  # 0=General, 1=Inbound, 2=Outbound
    interactive_format = Column(Integer, default=1)  # 1=Guided, 2=Unguided
    compliance = Column(Boolean, nullable=False, default=False)  # 0=No, 1=Yes
    ai_version = Column(Integer, nullable=True)
    rule_engine = Column(String(255), default='1.0')  # Default is '1.0' and new is '1.1'
    coaching = Column(String(255), default='1.0')
    user_workbench_version = Column(String(10), nullable=False, default='v1')  # Specifies version of user workbench enabled for this story

    #Relationships
    #guide = relationship("Video", back_populates="stories")
    #owner = relationship("User", back_populates="stories")


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    username = Column(String(255))
    title = Column(String(127))
    firstName = Column(String(255))
    lastName = Column(String(255))
    email = Column(String(255), unique=True)
    secondary_email = Column(String(255))
    defaultEmail = Column(TINYINT(1), comment='1= email, 2=secondary')
    password = Column(String(255))
    image = Column(LargeBinary)
    # account_id = Column(ForeignKey('account.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    last_login_time = Column(DateTime)
    created_time = Column(DateTime)
    inactive = Column(TINYINT(1), server_default=text("'0'"))
    inactive_datetime = Column(DateTime)
    # language_id = Column(ForeignKey('language.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)
    signature = Column(Text)
    coach_id = Column(ForeignKey('user.id'), index=True)
    secondary_coach_id = Column(ForeignKey('user.id'), index=True)
    timezone_offset = Column(Float)
    timezone = Column(INTEGER(11))
    brand_id = Column(INTEGER(11))
    terms_accepted_datetime = Column(TIMESTAMP)
    passwordchanged_time = Column(TIMESTAMP)
    otp = Column(String(255))
    thumbnail = Column(String(255))
    thumbnail = Column(String(255))
    jwt_access_token = Column(String(255))
    jwt_refresh_token = Column(String(255))
    previous_password = Column(Text)



class Brand(Base):
    __tablename__ = 'brand'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), index=True, nullable=False)
    inactive = Column(Boolean, default=False, nullable=False)
    created_by = Column(Integer, default=0)
    created_time = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    updated_by = Column(Integer, default=0)
    last_updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp(), nullable=True)
