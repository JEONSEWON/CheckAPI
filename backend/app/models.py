"""
SQLAlchemy Database Models
"""

from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from app.database import Base

# Use String(36) for SQLite compatibility instead of UUID
def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    name = Column(String(100))
    plan = Column(String(20), default="free")  # free, starter, pro, business
    stripe_customer_id = Column(String(100))
    is_active = Column(Boolean, default=True)
    onboarding_completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    monitors = relationship("Monitor", back_populates="user", cascade="all, delete-orphan")
    alert_channels = relationship("AlertChannel", back_populates="user", cascade="all, delete-orphan")
    subscription = relationship("Subscription", back_populates="user", uselist=False)
    api_keys = relationship("APIKey", back_populates="user", cascade="all, delete-orphan")
    maintenance_windows = relationship("MaintenanceWindow", back_populates="user", cascade="all, delete-orphan")
    # Team
    owned_team_members = relationship("TeamMember", foreign_keys="TeamMember.owner_id", back_populates="owner", cascade="all, delete-orphan")
    team_memberships = relationship("TeamMember", foreign_keys="TeamMember.member_id", back_populates="member")


class Monitor(Base):
    """Monitor model - represents a URL/API to monitor"""
    __tablename__ = "monitors"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    url = Column(String(2048), nullable=False)
    method = Column(String(10), default="GET")  # GET, POST, PUT, DELETE
    interval = Column(Integer, default=300)  # seconds (5 minutes)
    timeout = Column(Integer, default=30)  # seconds
    headers = Column(JSON)  # custom headers
    body = Column(Text)  # for POST/PUT requests
    expected_status = Column(Integer, default=200)
    # Monitor type
    monitor_type = Column(String(20), default="http")  # http, heartbeat

    # Heartbeat fields (null for http monitors)
    heartbeat_token = Column(String(64), unique=True, nullable=True)
    heartbeat_interval = Column(Integer, nullable=True)  # expected ping interval in minutes
    heartbeat_grace = Column(Integer, nullable=True, default=5)  # grace period in minutes
    last_ping_at = Column(DateTime, nullable=True)

    # Response body validation
    keyword = Column(String(500))
    keyword_present = Column(Boolean, default=True)
    use_regex = Column(Boolean, default=False)
    # SSL monitoring
    ssl_check = Column(Boolean, default=True)
    ssl_expiry_days = Column(Integer, default=14)
    ssl_expires_at = Column(DateTime)
    ssl_last_checked = Column(DateTime)
    # Alert threshold — N consecutive failures before alerting (default 1 = alert immediately)
    alert_threshold = Column(Integer, default=1)
    consecutive_failures = Column(Integer, default=0)
    alert_sent = Column(Boolean, default=False)  # True while an ongoing incident alert has been sent
    # Custom domain for public status page (Pro/Business)
    custom_domain = Column(String(255), unique=True, nullable=True)

    is_active = Column(Boolean, default=True, index=True)
    last_status = Column(String(20))  # up, down, degraded
    last_checked_at = Column(DateTime)
    next_check_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="monitors")
    checks = relationship("Check", back_populates="monitor", cascade="all, delete-orphan")
    alert_channels = relationship("AlertChannel", secondary="monitor_alert_channels", back_populates="monitors")
    maintenance_windows = relationship("MaintenanceWindow", secondary="maintenance_window_monitors", back_populates="monitors")
    assertions = relationship("MonitorAssertion", back_populates="monitor", cascade="all, delete-orphan", order_by="MonitorAssertion.order")


class Check(Base):
    """Check model - represents a single health check result"""
    __tablename__ = "checks"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    monitor_id = Column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), nullable=False)  # up, down, degraded
    status_code = Column(Integer)
    response_time = Column(Integer)  # milliseconds
    error_message = Column(Text)
    checked_at = Column(DateTime, default=datetime.utcnow, index=True)
    ai_analysis = Column(JSON, nullable=True)

    # Relationships
    monitor = relationship("Monitor", back_populates="checks")


class AlertChannel(Base):
    """Alert Channel model - email, slack, telegram, etc."""
    __tablename__ = "alert_channels"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    type = Column(String(20), nullable=False)  # email, slack, telegram, discord, webhook
    config = Column(JSON, nullable=False)  # channel-specific config
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="alert_channels")
    monitors = relationship("Monitor", secondary="monitor_alert_channels", back_populates="alert_channels")


class MonitorAlertChannel(Base):
    """Many-to-Many relationship between Monitors and AlertChannels"""
    __tablename__ = "monitor_alert_channels"
    
    monitor_id = Column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), primary_key=True)
    alert_channel_id = Column(String(36), ForeignKey("alert_channels.id", ondelete="CASCADE"), primary_key=True)


class TeamMember(Base):
    """Team member - links a member user to an owner user"""
    __tablename__ = "team_members"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    owner_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    member_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)  # null until accepted
    invited_email = Column(String(255), nullable=False)
    role = Column(String(20), default="member")  # owner, member
    status = Column(String(20), default="pending")  # pending, active
    invite_token = Column(String(100), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime)

    # Relationships
    owner = relationship("User", foreign_keys=[owner_id], back_populates="owned_team_members")
    member = relationship("User", foreign_keys=[member_id], back_populates="team_memberships")


class Subscription(Base):
    """Subscription model - user's payment subscription"""
    __tablename__ = "subscriptions"
    
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    lemonsqueezy_subscription_id = Column(String(100), unique=True)
    plan = Column(String(20), nullable=False)  # free, starter, pro, business
    status = Column(String(20), nullable=False)  # active, canceled, past_due
    current_period_end = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="subscription")

class APIKey(Base):
    """API Key model - for Business plan programmatic access"""
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(100), nullable=False)
    key_hash = Column(String(255), nullable=False, unique=True)
    key_prefix = Column(String(10), nullable=False)
    last_used_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="api_keys")


class MaintenanceWindow(Base):
    """Maintenance Window - suppress alerts during scheduled maintenance"""
    __tablename__ = "maintenance_windows"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    repeat_type = Column(String(20), default="once")  # once, daily, weekly, monthly
    weekday = Column(Integer)  # 0=Mon ~ 6=Sun (weekly only)
    day_of_month = Column(Integer)  # 1-31 (monthly only)
    start_time = Column(String(5), nullable=False)  # HH:MM
    end_time = Column(String(5), nullable=False)    # HH:MM
    start_date = Column(DateTime)  # once only
    end_date = Column(DateTime)    # once only
    timezone = Column(String(50), default="UTC")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="maintenance_windows")
    monitors = relationship("Monitor", secondary="maintenance_window_monitors", back_populates="maintenance_windows")


class MaintenanceWindowMonitor(Base):
    """Many-to-Many: MaintenanceWindow <-> Monitor"""
    __tablename__ = "maintenance_window_monitors"

    maintenance_window_id = Column(String(36), ForeignKey("maintenance_windows.id", ondelete="CASCADE"), primary_key=True)
    monitor_id = Column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), primary_key=True)


class AuditLog(Base):
    """Audit log — records user-initiated actions on monitors and alert channels."""
    __tablename__ = "audit_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(50), nullable=False, index=True)  # monitor.create, monitor.delete, etc.
    resource_type = Column(String(50))  # monitor, alert_channel, subscription, ...
    resource_id = Column(String(36))
    detail = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class WebhookLog(Base):
    """Log of incoming LemonSqueezy webhook events for debugging and auditing."""
    __tablename__ = "webhook_logs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_name = Column(String(100), nullable=False, index=True)
    lemonsqueezy_subscription_id = Column(String(100))
    user_id = Column(String(36))
    payload = Column(JSON, nullable=False)
    processed_at = Column(DateTime, default=datetime.utcnow, index=True)
    success = Column(Boolean, default=True)
    error_message = Column(Text)


class MonitorAssertion(Base):
    """Assertion model - response validation rules per monitor"""
    __tablename__ = "monitor_assertions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    monitor_id = Column(String(36), ForeignKey("monitors.id", ondelete="CASCADE"), nullable=False)
    assertion_type = Column(String(20), nullable=False, default="jsonpath")  # keyword, jsonpath
    path = Column(Text, nullable=True)           # JSON Path e.g. $.data.status
    operator = Column(String(20), nullable=False) # ==, !=, >, >=, <, <=, contains, not_contains, is_null, is_not_null, exists
    value = Column(JSON, nullable=True)           # expected value (string/number/bool/null)
    logic = Column(String(3), default="AND")      # AND / OR
    order = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    monitor = relationship("Monitor", back_populates="assertions")
