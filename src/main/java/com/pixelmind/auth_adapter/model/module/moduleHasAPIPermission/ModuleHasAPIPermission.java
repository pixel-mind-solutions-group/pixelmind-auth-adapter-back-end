//package com.pixelmind.auth_adapter.model.module.moduleHasAPIPermission;
//
//import com.pixelmind.auth_adapter.model.AuditData;
//import com.pixelmind.auth_adapter.model.module.Module;
//import com.pixelmind.auth_adapter.model.permission.api.APIPermission;
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
//@Entity
//@NoArgsConstructor
//@AllArgsConstructor
//@Table
//public class ModuleHasAPIPermission {
//    @Id
//    @GeneratedValue(generator = "UUID")
//    @GenericGenerator(
//        name = "UUID",
//        strategy = "org.hibernate.id.UUIDGenerator"
//    )
//    @Column(updatable = false, nullable = false)
//    private UUID id;
//
//    @ManyToOne
//    @JoinColumn(name = "module_id")
//    private Module module;
//
//    @ManyToOne
//    @JoinColumn(name = "api_permission_id")
//    private APIPermission apiPermission;
//
//    @Embedded
//    @AttributeOverrides(value = {
//            @AttributeOverride(name = "createdBy", column = @Column(name = "created_by")),
//            @AttributeOverride(name = "createdOn", column = @Column(name = "created_on"))
//    })
//    private AuditData auditData;
//}
