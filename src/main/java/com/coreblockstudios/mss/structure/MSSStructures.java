package com.coreblockstudios.mss.structure;

import com.coreblockstudios.mss.MSS;
import net.minecraft.core.registries.Registries;
import net.minecraft.world.level.levelgen.structure.StructureType;
import net.minecraft.world.level.levelgen.structure.pools.StructureTemplatePool;
import net.neoforged.neoforge.registries.DeferredRegister;

import java.util.function.Supplier;

public class MSSStructures {
    public static final DeferredRegister<StructureType<?>> STRUCTURE_TYPES =
            DeferredRegister.create(Registries.STRUCTURE_TYPE, MSS.MODID);

    public static final DeferredRegister<StructureTemplatePool> TEMPLATE_POOLS =
            DeferredRegister.create(Registries.TEMPLATE_POOL, MSS.MODID);

    public static void register(net.neoforged.bus.api.IEventBus bus) {
        STRUCTURE_TYPES.register(bus);
        TEMPLATE_POOLS.register(bus);
    }
}
