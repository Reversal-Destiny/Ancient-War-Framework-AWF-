# -*- coding: utf-8 -*-

from AncientWarFramework.Core.UI.Feature import UIInfrastructureFeature
from AncientWarFramework.Domain.Faction import FactionFeature
from AncientWarFramework.Domain.Soldier import SoldierFeature
from AncientWarFramework.Domain.Ownership import OwnershipFeature
from AncientWarFramework.Domain.Formation import FormationFeature
from AncientWarFramework.Domain.CombatRelation import CombatRelationFeature
from AncientWarFramework.Domain.Command import CommandFeature
from AncientWarFramework.Domain.Resource import ResourceFeature
from AncientWarFramework.Domain.Building import BuildingFeature
from AncientWarFramework.Domain.Workbench import WorkbenchFeature
from AncientWarFramework.Domain.Technology import TechnologyFeature
from AncientWarFramework.Domain.Spawn import SpawnFeature
from AncientWarFramework.Domain.Patrol import PatrolFeature

STANDARD_DOMAIN_FEATURES = (
    UIInfrastructureFeature,
    FactionFeature,
    SoldierFeature,
    OwnershipFeature,
    FormationFeature,
    CombatRelationFeature,
    CommandFeature,
    ResourceFeature,
    BuildingFeature,
    WorkbenchFeature,
    TechnologyFeature,
    SpawnFeature,
    PatrolFeature,
)
