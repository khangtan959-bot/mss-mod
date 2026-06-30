package com.coreblockstudios.mss;

import com.coreblockstudios.mss.item.MSSItems;
import com.coreblockstudios.mss.item.MSSCreativeTab;
import com.coreblockstudios.mss.entity.MSSEntities;
import com.coreblockstudios.mss.structure.MSSStructures;
import com.coreblockstudios.mss.config.MSSConfig;
import net.minecraft.resources.ResourceLocation;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.ModLoadingContext;
import net.neoforged.fml.common.Mod;
import net.neoforged.fml.config.ModConfig;

@Mod(MSS.MODID)
public class MSS {
    public static final String MODID = "mss";

    public MSS(IEventBus modEventBus) {
        ModLoadingContext.get().registerConfig(ModConfig.Type.COMMON, MSSConfig.SPEC);

        MSSItems.register(modEventBus);
        MSSEntities.register(modEventBus);
        MSSStructures.register(modEventBus);
        MSSCreativeTab.register(modEventBus);
    }

    public static ResourceLocation id(String path) {
        return ResourceLocation.fromNamespaceAndPath(MODID, path);
    }
}
