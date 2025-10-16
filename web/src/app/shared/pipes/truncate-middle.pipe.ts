import { Pipe, PipeTransform } from "@angular/core";

@Pipe({ name: 'truncateMiddle' })
export class TruncateMiddlePipe implements PipeTransform {
    transform(value: string, maxLength = 25, front = 11, back = 11): string {
        if (!value) return '';
        if (value.length <= maxLength) return value;
        const start = value.slice(0, front);
        const end = value.slice(-back);
        return `${start}...${end}`;
    }
}