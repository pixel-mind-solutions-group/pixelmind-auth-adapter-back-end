//package com.pixelmind.auth_adapter.model.client;
//
//import com.pixelmind.auth_adapter.model.AuditData;
//import jakarta.persistence.*;
//import lombok.AllArgsConstructor;
//import lombok.Getter;
//import lombok.NoArgsConstructor;
//import lombok.Setter;
//import org.hibernate.annotations.GenericGenerator;
//import org.hibernate.annotations.UuidGenerator;
//
//import java.util.UUID;
//
//@Getter
//@Setter
//@NoArgsConstructor
//@AllArgsConstructor
//@Entity
//@Table(name = "client")
//public class Client {
//    @Id
//    @GeneratedValue(generator = "UUID")
//    @GenericGenerator(
//        name = "UUID",
//        strategy = "org.hibernate.id.UUIDGenerator"
//    )
//    @Column(updatable = false, nullable = false)
//    private UUID id;
//    private String clientId;
//    private Boolean active;
//
//    @Embedded
//    @AttributeOverrides(value = {
//            @AttributeOverride(name = "createdBy", column = @Column(name = "created_by")),
//            @AttributeOverride(name = "createdOn", column = @Column(name = "created_on")),
//            @AttributeOverride(name = "updatedBy", column = @Column(name = "updated_by")),
//            @AttributeOverride(name = "updatedOn", column = @Column(name = "updated_on"))
//    })
//    private AuditData auditData;
//}
