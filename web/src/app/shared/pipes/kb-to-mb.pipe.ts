import { Pipe, PipeTransform } from "@angular/core";

@Pipe({ name: 'kbToMb' })
export class KbToMb implements PipeTransform {
    transform(value: number, decimals = 2): string {
        if (!value && value !== 0) return '';
        const mb = (value / 1024)/1024;
        return `${mb.toFixed(decimals)} MB`;
    }
}