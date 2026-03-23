package com.pixelmind.auth_adapter.mapper;

import com.pixelmind.auth_adapter.dto.user.UserRequestDTO;
import com.pixelmind.auth_adapter.dto.user.UserResponseDTO;
import com.pixelmind.auth_adapter.model.user.User;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
public class UserMapper {

    public User toEntity(User user, UserRequestDTO userRequest) {
        user.setEmail(userRequest.getEmail());
        user.setFirstName(userRequest.getFirstName());
        user.setLastName(userRequest.getLastName());
        user.setEnabled(userRequest.getEnabled());
        user.setEmailVerified(userRequest.getEmailVerified());
        return user;
    }

    public UserResponseDTO toDTO(UserResponseDTO dto, User user) {
        dto.setId(String.valueOf(user.getId()));
        dto.setUsername(user.getUserName());
        dto.setEmail(user.getEmail());
        dto.setFirstName(user.getFirstName());
        dto.setLastName(user.getLastName());
        dto.setEnabled(user.isEnabled());
        dto.setEmailVerified(user.isEmailVerified());
        dto.setCreatedDate(user.getAuditData().getCreatedOn().toLocalDate());
        return dto;
    }

    public List<UserResponseDTO> toDTOs(List<User> userList) {
        return userList.stream()
                .map(u -> toDTO(new UserResponseDTO(), u))
                .toList();
    }
}
