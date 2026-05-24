package com.pixelmind.auth_adapter.service;

import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.application.ApplicationRequestDTO;

public interface ApplicationService {

    CommonResponseDTO createOrModify(String realmName, ApplicationRequestDTO applicationRequest);
}
