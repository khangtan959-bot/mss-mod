package com.coreblockstudios.mss.entity;

import com.coreblockstudios.mss.MSS;
import com.coreblockstudios.mss.entity.custom.*;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class MSSEntities {
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(BuiltInRegistries.ENTITY_TYPE, MSS.MODID);

    public static final DeferredHolder<EntityType<?>, EntityType<Mummy>> MUMMY =
            ENTITIES.register("mummy", () -> EntityType.Builder.of(Mummy::new, MobCategory.MONSTER)
                    .sized(0.6F, 1.9F).clientTrackingRange(8).build("mummy"));

    public static final DeferredHolder<EntityType<?>, EntityType<Spirit>> SPIRIT =
            ENTITIES.register("spirit", () -> EntityType.Builder.of(Spirit::new, MobCategory.MONSTER)
                    .sized(0.6F, 1.9F).clientTrackingRange(8).build("spirit"));

    public static final DeferredHolder<EntityType<?>, EntityType<QueenSpider>> QUEEN_SPIDER =
            ENTITIES.register("queen_spider", () -> EntityType.Builder.of(QueenSpider::new, MobCategory.MONSTER)
                    .sized(1.4F, 0.9F).clientTrackingRange(10).build("queen_spider"));

    public static final DeferredHolder<EntityType<?>, EntityType<SpiderWebProjectile>> SPIDER_WEB =
            ENTITIES.register("spider_web", () -> EntityType.Builder.<SpiderWebProjectile>of(
                            SpiderWebProjectile::new, MobCategory.MISC)
                    .sized(0.3F, 0.3F).clientTrackingRange(4).build("spider_web"));

    public static void register(net.neoforged.bus.api.IEventBus bus) {
        ENTITIES.register(bus);
    }
}
