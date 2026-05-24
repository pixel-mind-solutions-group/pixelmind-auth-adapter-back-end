package com.pixelmind.auth_adapter.service.impl;

import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.PageResponse;
import com.pixelmind.auth_adapter.dto.user.UserRequestDTO;
import com.pixelmind.auth_adapter.exception.BaseException;
import com.pixelmind.auth_adapter.mapper.UserMapper;
import com.pixelmind.auth_adapter.model.AuditData;
import com.pixelmind.auth_adapter.model.user.User;
import com.pixelmind.auth_adapter.repository.UserRepository;
import com.pixelmind.auth_adapter.repository.specification.UserSpecification;
import com.pixelmind.auth_adapter.service.UserService;
import lombok.RequiredArgsConstructor;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.UUID;

@RequiredArgsConstructor
@Service
public class UserServiceImpl implements UserService {

    private final UserRepository userRepository;
    private final UserMapper userMapper;

    @Override
    public CommonResponseDTO createOrModify(UserRequestDTO userRequest) {

        User user = new User();

        if (userRequest.getId() != null) {
            user = userRepository.findById(UUID.fromString(userRequest.getId()))
                    .orElseThrow(() -> new BaseException(HttpStatus.NOT_FOUND.value(), "User not found")
                    );
            user.getAuditData().setUpdatedBy("admin");
            user.getAuditData().setUpdatedOn(LocalDateTime.now());

        } else {
            AuditData auditData = new AuditData();

            user.setFailCount((short) 0);
            user.setUserName(userRequest.getUsername());
            user.setAuditData(auditData);
            auditData.setCreatedBy("admin");
            auditData.setCreatedOn(LocalDateTime.now());
        }

        userRepository.save(userMapper.toEntity(user, userRequest));

        return new CommonResponseDTO(
                HttpStatus.CREATED.value(),
                null,
                "User created success"
        );
    }

    @Override
    public CommonResponseDTO search(String searchParam,
                                    Integer page,
                                    Integer size) {

        Page<User> userPage = userRepository.findAll(
                UserSpecification.searchByParam(searchParam),
                PageRequest.of(page, size, Sort.by("auditData.createdOn").descending())
        );

        return new CommonResponseDTO(
                HttpStatus.OK.value(),
                PageResponse.builder()
                        .currentPage(userPage.getNumber())
                        .totalPages(userPage.getTotalPages())
                        .totalElements(userPage.getTotalElements())
                        .dataList(userMapper.toDTOs(userPage.getContent()))
                        .build(),
                "User list retrieved"
        );
    }
}
