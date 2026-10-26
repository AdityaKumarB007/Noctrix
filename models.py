from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

@dataclass
class NHI:
    """Normalized Non-Human Identity model used across all NOCTRIX layers."""
    id: str                                  # Unique deterministic ID, e.g., 'aws:iam:role:AdminRole'
    name: str                                # Human-readable name
    type: str                                # 'IAM_ROLE', 'IAM_USER', 'SERVICE_ACCOUNT', 'API_KEY', 'SERVICE_PRINCIPAL'
    provider: str                            # 'aws', 'k8s', 'git', 'azure', 'gcp'
    privilege_level: float = 0.0             # Normalized permission score (0.0=read-only, 1.0=full admin)
    last_active: Optional[str] = None        # ISO-8601 timestamp of last recorded activity
    owner: Optional[str] = None              # Assigned team, user, or None if unowned
    exposures: List[str] = field(default_factory=list)  # File paths or repos where secret was leaked
    risk_score: float = 0.0                  # Evaluated risk score between 0.0 and 100.0
    is_ghost: bool = False                   # True if orphaned & inactive >= 90 days
    remediated: bool = False                 # True if remediation action was executed
    remediated_at: Optional[str] = None      # ISO-8601 timestamp of remediation
    policies: List[str] = field(default_factory=list)    # Attached permissions / policies
    resources: List[str] = field(default_factory=list)   # Resources accessed (e.g. S3 buckets, namespaces)
    created_by: Optional[str] = None         # Creating user or system account

    def to_dict(self) -> Dict[str, Any]:
        """Convert NHI instance to a dictionary for graph serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "provider": self.provider,
            "privilege_level": self.privilege_level,
            "last_active": self.last_active or "",
            "owner": self.owner or "",
            "exposures": self.exposures,
            "risk_score": self.risk_score,
            "is_ghost": self.is_ghost,
            "remediated": self.remediated,
            "remediated_at": self.remediated_at or "",
            "policies": self.policies,
            "resources": self.resources,
            "created_by": self.created_by or "",
        }

@dataclass
class RemediationResult:
    """Outcome record of an automated remediation action."""
    nhi_id: str                              # Target NHI identifier
    action_type: str                         # 'VAULT_ROTATION' or 'AWS_KEY_DEACTIVATION'
    status: str                              # 'SUCCESS', 'FAILED', or 'BLOCKED_BY_ALLOWLIST'
    timestamp: str                           # ISO-8601 execution timestamp
    details: str                             # Diagnostic info or error description
    alert_sent: bool = False                 # True if Slack alert was dispatched

    def to_dict(self) -> Dict[str, Any]:
        return {
            "nhi_id": self.nhi_id,
            "action_type": self.action_type,
            "status": self.status,
            "timestamp": self.timestamp,
            "details": self.details,
            "alert_sent": self.alert_sent,
        }

@dataclass
class GraphRelationship:
    """Relationship edge connecting two entities in the Neo4j graph."""
    source_id: str                           # Source node ID
    target_id: str                           # Target node ID
    rel_type: str                            # 'USES', 'HAS_PERMISSION_ON', 'CREATED_BY'
    properties: Dict[str, Any] = field(default_factory=dict)
