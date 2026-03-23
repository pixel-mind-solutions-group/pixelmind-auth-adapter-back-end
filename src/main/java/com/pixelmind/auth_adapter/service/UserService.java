package com.pixelmind.auth_adapter.service;

import com.pixelmind.auth_adapter.dto.CommonResponseDTO;
import com.pixelmind.auth_adapter.dto.user.UserRequestDTO;

public interface UserService {

    CommonResponseDTO createOrModify(UserRequestDTO userRequest);

    CommonResponseDTO search(String searchParam, Integer page, Integer size);
}
