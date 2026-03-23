package com.pixelmind.auth_adapter.repository.specification;

import com.pixelmind.auth_adapter.model.user.User;
import com.pixelmind.auth_adapter.util.CommonValidation;
import org.springframework.data.jpa.domain.Specification;

public class UserSpecification {

    public static Specification<User> searchByParam(String searchParam) {
        return (root, query, cb) -> {
            if (CommonValidation.stringNullValidation(searchParam)) {
                return cb.conjunction();
            }

            String pattern = "%" + searchParam.toLowerCase() + "%";

            return cb.or(
                    cb.like(cb.lower(root.get("userName")), pattern),
                    cb.like(cb.lower(root.get("firstName")), pattern),
                    cb.like(cb.lower(root.get("lastName")), pattern),
                    cb.like(cb.lower(root.get("email")), pattern)
            );
        };
    }
}
