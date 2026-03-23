//package com.pixelmind.auth_adapter.model.permission.api;
//
//import jakarta.persistence.*;
//import lombok.AllArgsConstructor;
//import lombok.Getter;
//import lombok.NoArgsConstructor;
//import lombok.Setter;
//import org.hibernate.annotations.GenericGenerator;
//import org.hibernate.annotations.UuidGenerator;
//
//@Getter
//@Setter
//@Entity
//@NoArgsConstructor
//@AllArgsConstructor
//@Table
//public class APIPermission {
//    @Id
//    @GeneratedValue(generator = "UUID")
//    @GenericGenerator(
//        name = "UUID",
//        strategy = "org.hibernate.id.UUIDGenerator"
//    )
//    @Column(updatable = false, nullable = false)
//    private Integer id;
//    private String name;
//    private String description;
//}
