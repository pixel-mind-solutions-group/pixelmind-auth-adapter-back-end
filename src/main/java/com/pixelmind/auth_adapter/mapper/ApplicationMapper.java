package com.pixelmind.auth_adapter.mapper;

import com.pixelmind.auth_adapter.dto.application.ApplicationRequestDTO;
import com.pixelmind.auth_adapter.dto.application.ApplicationResponseDTO;
import com.pixelmind.auth_adapter.model.client.Client;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class ApplicationMapper {

    public Client toEntity(Client client, ApplicationRequestDTO applicationRequest) {
        client.setActive(applicationRequest.isEnabled());
        client.setClientId(applicationRequest.getClientId());
        client.setDescription(applicationRequest.getDescription());
        return client;
    }

    public ApplicationResponseDTO toDTO(ApplicationResponseDTO dto, Client client) {
        dto.setId(String.valueOf(client.getId()));
        dto.setClientId(client.getClientId());
        dto.setDescription(client.getDescription());
        dto.setActive(client.getActive());
        return dto;
    }

    public List<ApplicationResponseDTO> toDTOs(List<Client> clientList) {
        return clientList.stream()
                .map(a -> toDTO(new ApplicationResponseDTO(), a))
                .toList();
    }
}
