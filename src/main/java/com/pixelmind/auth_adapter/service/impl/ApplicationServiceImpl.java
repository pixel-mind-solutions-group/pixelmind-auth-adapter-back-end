package com.pixelmind.auth_adapter.service.impl;

import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.application.ApplicationRequestDTO;
import com.pixelmind.auth_adapter.dto.client.ClientResponseDTO;
import com.pixelmind.auth_adapter.exception.BaseException;
import com.pixelmind.auth_adapter.mapper.ApplicationMapper;
import com.pixelmind.auth_adapter.model.AuditData;
import com.pixelmind.auth_adapter.model.client.Client;
import com.pixelmind.auth_adapter.repository.ApplicationRepository;
import com.pixelmind.auth_adapter.service.ApplicationService;
import com.pixelmind.auth_adapter.service.rest.ApplicationClientService;
import com.pixelmind.auth_adapter.util.CommonValidation;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.UUID;

@Service
@RequiredArgsConstructor
public class ApplicationServiceImpl implements ApplicationService {

    private final ApplicationRepository applicationRepository;
    private final ApplicationMapper applicationMapper;
    private final ApplicationClientService applicationClientService;

    @Override
    public CommonResponseDTO createOrModify(String realmName, ApplicationRequestDTO applicationRequest) {

        Client client = new Client();
        String message;

        if (!CommonValidation.stringNullValidation(applicationRequest.getId())) {

            message = "Application updated success";

            client = applicationRepository.findById(UUID.fromString(applicationRequest.getId()))
                    .orElseThrow(() -> new BaseException(HttpStatus.NOT_FOUND.value(), "Client not found"));

            client.getAuditData().setUpdatedOn(LocalDateTime.now());
            client.getAuditData().setUpdatedBy("Admin");

            // Calling keycloak adapter to update client
            //TODO: update client in keycloak

        } else {

            // Calling keycloak adapter to create a client
            ClientResponseDTO createdClient = applicationClientService.createApplication(realmName, applicationRequest);
            client.setClientUUID(createdClient.getClientUUID());
            client.setRealmName(realmName);
            message = "Application created success";

            AuditData auditData = new AuditData();
            auditData.setCreatedOn(LocalDateTime.now());
            auditData.setCreatedBy("Admin");
            client.setAuditData(auditData);
        }

        applicationRepository.save(applicationMapper.toEntity(client, applicationRequest));

        return new CommonResponseDTO(
                HttpStatus.CREATED.value(),
                null,
                message
        );
    }
}
