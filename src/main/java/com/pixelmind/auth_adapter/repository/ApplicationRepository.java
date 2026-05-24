package com.pixelmind.auth_adapter.repository;

import com.pixelmind.auth_adapter.model.client.Client;
import com.pixelmind.auth_adapter.model.user.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.JpaSpecificationExecutor;
import org.springframework.stereotype.Repository;

import java.util.UUID;

@Repository
public interface ApplicationRepository extends JpaRepository<Client, UUID>, JpaSpecificationExecutor<User> {

}
