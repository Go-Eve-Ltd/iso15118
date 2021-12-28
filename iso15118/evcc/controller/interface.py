"""
This module contains the abstract class for an EVCC to retrieve data from the EV.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Tuple, Union

from iso15118.shared.messages.enums import Protocol
from iso15118.shared.messages.iso15118_2.datatypes import (
    ACEVChargeParameter,
    ChargeProgress,
    DCEVChargeParameter,
    EnergyTransferMode,
    EnergyTransferModeEnum,
    ProfileEntry,
    SAScheduleTuple,
)
from iso15118.shared.messages.iso15118_20.ac import (
    ACChargeParameterDiscoveryReqParams,
    BPTACChargeParameterDiscoveryReqParams,
)
from iso15118.shared.messages.iso15118_20.common_messages import EMAID


@dataclass
class ChargeParamsV2:
    energy_mode: EnergyTransferModeEnum
    ac_parameters: Optional[ACEVChargeParameter]
    dc_parameters: Optional[DCEVChargeParameter]


class EVControllerInterface(ABC):
    @abstractmethod
    def get_evcc_id(self, protocol: Protocol, iface: str) -> str:
        """
        Retrieves the EVCCID, which is a field of the SessionSetupReq. The structure of
        the EVCCID depends on the protocol version. In DIN SPEC 70121 and ISO 15118-2,
        the EVCCID is the MAC address (given as hexadecimal bytes), in ISO 15118-20 it's
        similar to a VIN (Vehicle Identification Number, given as str).

        Args:
            protocol: The communication protocol, a member of the Protocol enum
            iface (str): The network interface selected

        Raises:
            InvalidProtocolError

        Relevant for:
        - DIN SPEC 70121
        - ISO 15118-2
        - ISO 15118-20
        """
        raise NotImplementedError

    @abstractmethod
    def get_energy_transfer_mode(self) -> EnergyTransferModeEnum:
        """
        Gets the energy transfer mode requested for the current charging session.
        This depends on the charging cable being plugged in, which could be a
        Type 2 AC or Combo 2 plug, for example.

        Relevant for:
        - DIN SPEC 70121
        - ISO 15118-2
        """
        raise NotImplementedError

    @abstractmethod
    def get_charge_params_v2(self) -> ChargeParamsV2:
        """
        Gets the charge parameter needed for ChargeParameterDiscoveryReq (ISO 15118-2),
        including the energy transfer mode and the energy mode-specific parameters,
        which is an instance of either ACEVChargeParameter or DCEVChargeParameter,
        depending on the EnergyTransferMode.

        Returns:
            A tuple of ChargeParamsV2, including EnergyTransferMode and
            ACEVChargeParameter (or DCEVChargeParameter)

        Relevant for:
        - ISO 15118-2
        """
        raise NotImplementedError

    @abstractmethod
    def get_charge_params_v20(
        self,
    ) -> Tuple[
        ACChargeParameterDiscoveryReqParams,
        Optional[BPTACChargeParameterDiscoveryReqParams],
    ]:
        """
        Gets the charge parameters needed for a ChargeParameterDiscoveryReq, which is
        either an ACChargeParameterDiscoveryReq, or a DCChargeParameterDiscoveryReq,
        or a WPTChargeParameterDiscoveryReq from ISO 15118-20, including the optional
        optional BPT (bi-directional power flow) paramters.

        Returns:
            A tuple containing both the non-BPT and BPT charger parameter needed for a
            request message of type ChargeParameterDiscoveryReq (AC, DC, or WPT)

        Relevant for:
        - ISO 15118-20
        TODO Add support for DC and WPT in the return type
        """
        raise NotImplementedError

    @abstractmethod
    def is_cert_install_needed(self) -> bool:
        """
        Returns True if the installation of a contract certificate is needed, False
        otherwise. A certificate installation is needed if the authorization option
        'Contract' (Plug & Charge) is chosen but no valid contract certificate is
        currently installed. An EV manufacturer might also choose to use the
        certificate installation process instead of a certificate update process
        available in ISO 15118-2 as there's no benefit of using the
        CertificateUpdateReq instead of the CertificateInstallationReq message.
        For example, you might want to choose to do a contract certificate
        installation if a certificate is about to expire (e.g. in two weeks).

        Relevant for:
        - ISO 15118-2
        - ISO 15118-20
        """
        raise NotImplementedError

    @abstractmethod
    def process_sa_schedules(
        self, sa_schedules: List[SAScheduleTuple]
    ) -> Tuple[ChargeProgress, int, List[ProfileEntry]]:
        """
        Processes the SAScheduleList provided with the ChargeParameterDiscoveryRes
        to decide which of the offered schedules to choose and whether or not to
        start charging instantly (ChargeProgress=Start) or to delay the charging
        process (ChargeProgress=Stop), including information on how the EV's
        charging profile will look like.

        Args:
            sa_schedules: The list of offered charging profiles (SAScheduleTuple
                          elements), each of which contains a mandatory PMaxSchedule
                          and an optional SalesTariff

        Returns:
            A tuple consisting of
            1. the ChargeProgress status,
            2. the ID of the chosen charging schedule (SAScheduleTuple), and
            3. the resulting charging profile of the EV, which may follow the
               suggestion of the offered charging schedule exactly or deviate
               (consume less power, but never more than the max limit provided by
               the SECC).

        Relevant for:
        - ISO 15118-2
        """
        raise NotImplementedError

    @abstractmethod
    def continue_charging(self) -> bool:
        """
        Whether or not to continue the energy flow during the charging loop. This
        depends on factors like SOC or user interaction with the vehicle (e.g. opened
        doors). If True, the charging loop continues.

        Relevant for:
        - DIN SPEC 70121
        - ISO 15118-2
        - ISO 15118-20
        """
        raise NotImplementedError

    @abstractmethod
    def store_contract_cert_and_priv_key(self, contract_cert: bytes, priv_key: bytes):
        """
        Stores the contract certificate and associated private key, both needed
        for Plug & Charge and received via a CertificateInstallationRes.
        This is a mockup, but a real EV should interact with a hardware security
        module (HSM) on a productive environment.

        Relevant for:
        - ISO 15118-2
        - ISO 15118-20
        """
        raise NotImplementedError

    @abstractmethod
    def get_prioritised_emaids(self) -> Optional[List[EMAID]]:
        """
        Indicates the list of EMAIDs (E-Mobility Account IDs) referencing contract
        certificates that shall be installed into the EV. The EMAIDs are given in
        the order of priority from highest priority to lowest priority.
        The secondary actor (e.g. Contract Certificate Pool operator, see the spec
        VDE-AR-E 2802-100-1, implemented by e.g. Hubject) will use this parameter to
        filter the list of contract certificates to be installed in case
        MaximumContractCertificateChains (a parameter the EVCC sends in
        CertificateInstallationReq) is smaller than the number of contract
        certificates available and ensures that the EV gets the highest priority
        contract certificates it desires.

        Relevant for:
        - ISO 15118-20
        """
        raise NotImplementedError