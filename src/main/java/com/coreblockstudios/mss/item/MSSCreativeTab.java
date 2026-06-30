package com.coreblockstudios.mss.item;

import com.coreblockstudios.mss.MSS;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.ItemStack;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public class MSSCreativeTab {
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, MSS.MODID);

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> MSS_TAB = TABS.register("mss",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.mss"))
                    .icon(() -> new ItemStack(MSSItems.INFO_BOOK.get()))
                    .displayItems((params, output) -> {
                        output.accept(MSSItems.INFO_BOOK.get());
                        output.accept(MSSItems.MUMMY_SPAWN_EGG.get());
                        output.accept(MSSItems.SPIRIT_SPAWN_EGG.get());
                        output.accept(MSSItems.QUEEN_SPIDER_SPAWN_EGG.get());
                    })
                    .build());

    public static void register(net.neoforged.bus.api.IEventBus bus) {
        TABS.register(bus);
    }
}
